jQuery(document).ready(function ($) {
    // Функция для обновления списка моделей при изменении марки
    let updateModels = function () {
        console.log("Изменение марки обнаружено.");
        let selectedMarkId = $('#id_mark').val();
        console.log("Выбранная марка ID:", selectedMarkId);
        let modelField = $('#id_model');

        // Сохранение предыдущего выбранного значения модели
        let previousValue = modelField.val();

        // Запрос на сервер для получения моделей, связанных с выбранной маркой
        $.ajax({
            url: '/get_models_disassembly/', // Укажите URL, который будет обрабатывать запрос и возвращать модели
            data: {
                'mark_id': selectedMarkId
            },
            success: function (data) {
                console.log("Получены данные моделей:", data);
                // Обновление списка моделей
                modelField.empty(); // Очищаем список
                $.each(data, function (key, value) {
                    modelField.append('<option value="' + key + '">' + value + '</option>');
                });
                console.log("Список моделей успешно обновлен.");

                // Установка предыдущего выбранного значения
                modelField.val(previousValue);
            }
        });
    };

    // Вызов функции при изменении марки
    $('#id_mark').change(updateModels);

    // Вызов функции при загрузке страницы (чтобы модели обновились, если марка уже выбрана)
    updateModels();
});