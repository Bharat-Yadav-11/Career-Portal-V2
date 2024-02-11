function postJob() {

    const fields = [
        'job-title', 'job-description', 'job-expected-salary-range-minimum',
        'job-expected-salary-range-maximum', 'job-application-deadline',
        'job-sector', 'job-type', 'job-experience', 'job-qualification',
        'job-vacancy', 'job-skill', 'job-workplace-type', 'job-country',
        'job-state', 'job-city', 'job-complete-address', 'contact-name',
        'contact-email', 'contact-phone'
    ];

    let formData = new FormData();
    let emptyFields = [];

    fields.forEach(field => {
        let value = document.getElementById(field).value.trim();

        if (value === '') {
            emptyFields.push(field.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()));
        }

        if (field === 'job-expected-salary-range-minimum' || field === 'job-expected-salary-range-maximum') {
            value = parseFloat(value); // Convert to float for comparison
        }

        formData.append(field.replace(/-/g, ''), value);
    });

    // Check for empty fields
    if (emptyFields.length > 0) {
        showSystemMessage('Fill the following fields: ' + emptyFields.join(', '), 'error');
        return;
    }

    // Validate salary range
    const minSalary = formData.get('jobexpectedsalaryrangeminimum');
    const maxSalary = formData.get('jobexpectedsalaryrangemaximum');
    if (Number(minSalary) > Number(maxSalary)) {
        showSystemMessage('Minimum salary cannot be greater than maximum salary', 'error');
        return;
    }


    if (document.getElementById('job-post-terms').checked === false) {
        showSystemMessage('You must agree to the terms and conditions, before posting a job', 'error');
        return;
    }

    // Handle optional fields
    let optionalFields = ['alternate-phone', 'contact-linkedin'];
    optionalFields.forEach(field => {
        let value = formData.get(field.replace(/-/g, ''));
        if (value === '') {
            formData.set(field.replace(/-/g, ''), null);
        }
        else {
            formData.set(field.replace(/-/g, ''), value);
        }
    });

    grecaptcha.ready(function () {
        grecaptcha
            .execute("6LfTQOgnAAAAAPUKwxk5C_ZQNIi__k7HGTzbi3Yw", { action: "post_job" })
            .then(function (token) {
                console.log(token);
                formData.set('reCaptchaToken', token);


                fetch('/api/v1/organization/post-job', {
                    method: 'POST',
                    body: JSON.stringify(Object.fromEntries(formData)),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Career-Portal-CSRF-Token': getCSRFToken()
                    }
                }).then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            showSystemMessage(data.message, 'success');
                            document.location.href = '/organization/posted-jobs';
                        } else if (data.status === 'error') {
                            showSystemMessage(data.message, 'error');
                        }
                    }).catch(error => {
                        showSystemMessage('An error occurred while processing your request', 'error');
                    });

            }).catch(error => {
                console.log(error);
                showSystemMessage('The reCAPTCHA token could not be generated, please try again', 'error');
            });
    }
    );
}

