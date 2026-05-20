document.addEventListener('DOMContentLoaded', async () => {
    const loadingIndicator = document.getElementById('loading-indicator');
    const formFieldsContainer = document.getElementById('form-fields-container');
    const formActions = document.getElementById('form-actions');
    const form = document.getElementById('footprint-form');
    const resultSection = document.getElementById('result-section');
    const emissionValue = document.getElementById('emission-value');
    const recalculateBtn = document.getElementById('recalculate-btn');

    let schemaOptions = null;

    // Fetch options from backend
    try {
        const response = await fetch('/api/options');
        if (!response.ok) throw new Error("Failed to load schema options");
        schemaOptions = await response.json();
        
        buildForm(schemaOptions);
        
        // Hide loading, show form
        loadingIndicator.classList.add('hide');
        formFieldsContainer.classList.remove('hide');
        formActions.classList.remove('hide');
    } catch (err) {
        loadingIndicator.innerHTML = `<p style="color: red;">Error loading data. Is the backend running?</p>`;
        console.error(err);
    }

    // Build the form dynamically based on JSON
    function buildForm(data) {
        formFieldsContainer.innerHTML = '';

        // Add Categorical (Selects)
        for (const [key, options] of Object.entries(data.categorical)) {
            const group = document.createElement('div');
            group.className = 'form-group';
            
            const label = document.createElement('label');
            label.textContent = key;
            label.setAttribute('for', escapeId(key));
            
            const select = document.createElement('select');
            select.id = escapeId(key);
            select.name = key;
            select.required = true;

            options.forEach(opt => {
                const optionEl = document.createElement('option');
                optionEl.value = opt;
                optionEl.textContent = opt;
                select.appendChild(optionEl);
            });

            group.appendChild(label);
            group.appendChild(select);
            formFieldsContainer.appendChild(group);
        }

        // Add Numeric (Number Inputs)
        for (const [key, stats] of Object.entries(data.numeric)) {
            const group = document.createElement('div');
            group.className = 'form-group';
            
            const label = document.createElement('label');
            label.textContent = `${key} (avg: ${Math.round(stats.mean)})`;
            label.setAttribute('for', escapeId(key));
            
            const input = document.createElement('input');
            input.type = 'number';
            input.id = escapeId(key);
            input.name = key;
            input.min = stats.min;
            input.max = stats.max;
            input.step = 'any';
            input.value = Math.round(stats.mean); // Set default to mean
            input.required = true;

            group.appendChild(label);
            group.appendChild(input);
            formFieldsContainer.appendChild(group);
        }
    }

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitData = {};
        
        for (const [key, value] of formData.entries()) {
            // Check if it should be numeric based on our schema
            if (schemaOptions.numeric[key]) {
                submitData[key] = parseFloat(value);
            } else {
                submitData[key] = value;
            }
        }

        // Send predict request
        const btn = document.getElementById('calculate-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span>Calculating...</span>';
        btn.disabled = true;

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ features: submitData })
            });

            if (!response.ok) throw new Error("Calculation failed");
            const result = await response.json();
            
            // Show result
            animateValue(emissionValue, 0, result.carbon_emission_kg, 1500);
            
            form.classList.add('hide');
            resultSection.classList.remove('hide');

        } catch (err) {
            alert('Error calculating footprint: ' + err.message);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });

    recalculateBtn.addEventListener('click', () => {
        resultSection.classList.add('hide');
        form.classList.remove('hide');
    });

    // Helper: Escape space for HTML IDs
    function escapeId(str) {
        return str.replace(/\s+/g, '-').toLowerCase();
    }

    // Number animation helper
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = (progress * (end - start) + start).toFixed(2);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
