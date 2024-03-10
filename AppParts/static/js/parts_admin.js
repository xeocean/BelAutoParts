// Подкатегории

jQuery(document).ready(function ($) {

    // Функция для обновления списка подкатегорий при изменении категории
    let updateSubcategories = function () {
        console.log("Изменение категории обнаружено.");
        let selectedCategoryId = $('#id_category').val();
        console.log("Выбранная категория ID:", selectedCategoryId);
        let subcategoryField = $('#id_subcategory');

        // Сохранение предыдущего выбранного значения подкатегории
        let previousValue = subcategoryField.val();

        // Запрос на сервер для получения подкатегорий, связанных с выбранной категорией
        $.ajax({
            url: '/get_subcategories/', // Укажите URL, который будет обрабатывать запрос и возвращать подкатегории
            data: {
                'category_id': selectedCategoryId
            },
            success: function (data) {
                console.log("Получены данные подкатегорий:", data);
                // Обновление списка подкатегорий
                subcategoryField.empty(); // Очищаем список
                $.each(data, function (key, value) {
                    subcategoryField.append('<option value="' + key + '">' + value + '</option>');
                });
                console.log("Список подкатегорий успешно обновлен.");

                // Установка предыдущего выбранного значения
                subcategoryField.val(previousValue);
            }
        });
    };

    // Вызов функции при изменении категории
    $('#id_category').change(updateSubcategories);

    // Вызов функции при загрузке страницы (чтобы подкатегории обновились, если категория уже выбрана)
    updateSubcategories();
});

// Модели

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
            url: '/get_models/', // Укажите URL, который будет обрабатывать запрос и возвращать модели
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

