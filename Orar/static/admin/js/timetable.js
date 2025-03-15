document.addEventListener('DOMContentLoaded', function() {
    const classTypeField = document.querySelector('#id_class_type');
    const secondCourseFields = [
        document.querySelector('#id_second_course'),
        document.querySelector('#id_second_course_type'),
        document.querySelector('#id_second_instructor'),
        document.querySelector('#id_second_room'),
        document.querySelector('#id_second_week_type')
    ];

    function toggleFields() {
        const classType = classTypeField.value;
        if (classType === 'Single Class') {
            secondCourseFields.forEach(field => field.closest('.form-row').style.display = 'none');
        } else if (classType === 'Dual Class') {
            secondCourseFields.forEach(field => field.closest('.form-row').style.display = 'block');
        } else if (classType === 'Different Subgroups') {
            secondCourseFields.forEach(field => field.closest('.form-row').style.display = 'block');
        }
    }

    classTypeField.addEventListener('change', toggleFields);
    toggleFields();
});