document.addEventListener('DOMContentLoaded', () => {
    // 🌙 Dark mode toggle
    const toggle = document.querySelector('.dark-mode-toggle');
    toggle?.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    });

    // ⏳ Submit button loading effect
    const submit = document.getElementById('submitBtn');
    submit?.addEventListener('click', () => submit.classList.add('loading'));

    // 📡 IoT Sensor Logic
    const iotCheckbox = document.getElementById('iotCheckbox');
    const heartRateContainer = document.getElementById('heartRateContainer');
    const timerMessage = document.getElementById('timerMessage');
    const spo2Input = document.getElementById('spo2Input');
    const heartRateInput = document.getElementById('heartRateInput');

    iotCheckbox?.addEventListener('change', () => {
        if (iotCheckbox.checked) {
            heartRateContainer.style.display = 'block';
            timerMessage.style.display = 'block';
            timerMessage.textContent = '⏳ Fetching latest sensor data... Please wait.';

            fetch('/fetch_iot_data')
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'ok') {
                        spo2Input.value = data.spo2;
                        heartRateInput.value = data.heart_rate;
                        timerMessage.textContent = '✅ Data fetched successfully!';
                    } else if (data.status === 'finger_not_found') {
                        timerMessage.textContent = '🖐️ Finger not found. Please enter manually.';
                    } else {
                        timerMessage.textContent = '⚠️ Unable to fetch IoT data. Please enter manually.';
                    }
                })
                .catch(() => {
                    timerMessage.textContent = '⚠️ Error fetching IoT data. Please try again.';
                });
        } else {
            heartRateContainer.style.display = 'none';
            timerMessage.style.display = 'none';
        }
    });
});
