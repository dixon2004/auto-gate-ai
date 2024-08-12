document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.getElementById('flash-messages');
    console.log('Flash messages element:', flashMessages);
    
    if (flashMessages) {
        console.log('Starting fade-out');
        setTimeout(() => {
            flashMessages.style.opacity = '0';
            console.log('Opacity set to 0');
            setTimeout(() => {
                flashMessages.classList.add('fade-out');
                console.log('Flash messages removed');
            }, 1000);
        }, 5000);
    }
});


document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));

        this.classList.add('active');
        document.getElementById(this.dataset.tab).classList.add('active');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    function handleDeleteButtonClick() {
        const headers = document.querySelectorAll('table th');

        let phoneNumberIndex = -1;
        let licensePlateIndex = -1;
        let isExitTimeColumnPresent = false;

        Array.from(headers).forEach((header, index) => {
            const headerText = header.textContent.trim().toLowerCase();
            console.log('Header:', headerText);

            if (headerText === 'phone number') {
                phoneNumberIndex = index;
            } else if (headerText === 'license plate') {
                licensePlateIndex = index;
            } else if (headerText === 'exit time') {
                isExitTimeColumnPresent = true;
            }
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');

                const licensePlate = licensePlateIndex !== -1 ? 
                    row.querySelector(`td:nth-child(${licensePlateIndex + 1})`).textContent : null;
                const phoneNumber = phoneNumberIndex !== -1 ? 
                    row.querySelector(`td:nth-child(${phoneNumberIndex + 1})`).textContent : null;

                console.log('License Plate:', licensePlate);
                console.log('Phone Number:', phoneNumber);

                const endpoint = isExitTimeColumnPresent ? '/delete_visitor' : '/delete_resident';

                fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        license_plate: licensePlate,
                        phone_number: phoneNumber
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        row.remove();
                    } else {
                        alert('Error deleting record');
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }

    handleDeleteButtonClick();
});