// init original_thumbnail_urls var
const original_thumbnail_urls = {}

// * PAY ATTENTION * you have to define
//   const required_sizes = {
//      form.prefix: [parseInt({{ required_size.0 }}), parseInt({{ required_size.0 }})],
//   }
// at the template, because we need to take data from view context for dynamic validation


// kind of event listener for file inputs
const fileInputs = document.getElementsByClassName('form-control-file')

for (let i = 0; i < fileInputs.length; i++) {
    fileInputs[i].setAttribute('onchange', "validate_then_set_thumbnail(event)")
}


function validate_then_set_thumbnail(event) {
    const imageInput = event.currentTarget;
    const reader = new FileReader();

    reader.onload = function() {
        const required_size = required_sizes[`${imageInput.name.split('-')[0]}`]
        image_validation(reader.result, required_size, (is_valid) => {
            const thumbnail = document.getElementById(`${imageInput.id}-thumbnail`);

            if (is_valid) {
                original_thumb_url_backup(imageInput.name, thumbnail)
                thumbnail.src = reader.result;
                toggle_error(true, imageInput, required_size)

                toastr.success('Данные валидны');
            } else {
                original_thumb_url_backup(imageInput.name, thumbnail, true)
                toggle_error(false, imageInput, required_size)

                toastr.error('Данные невалидны');
            }
        })
    };

    reader.readAsDataURL(event.target.files[0]);
  }


function image_validation(src, required_size, callback) {
    const image = new Image();

    image.onload = function() {
        if (JSON.stringify([image.naturalWidth, image.naturalHeight]) === JSON.stringify(required_size)) {
            callback(true);
        } else {
            callback(false);
        }
    }
    image.src = src;
}


function toggle_error(validation_succeed, imageInput, required_size) {
    const imageField = imageInput.parentNode;

    if (validation_succeed) {
        if (imageField.lastElementChild.tagName === 'P') {
            imageInput.className = `${imageInput.className}`.replace(RegExp(' is-invalid'), '');
            imageField.removeChild(imageField.lastElementChild);
        }
    } else {
        if (imageField.lastElementChild.tagName !== 'P') {
            imageInput.className = `${imageInput.className} is-invalid`;

            const p = document.createElement("p");
            p.id = `error_1_${imageInput.id}`;
            p.className = "invalid-feedback";
            p.innerHTML = `<strong>Выберите изображение с разрешением ${required_size[0]}x${required_size[1]}</strong>`;

            imageField.append(p);
        }
    }
}


function original_thumb_url_backup(name, thumbnail, restore=false) {
    if (!restore) {
        if (!(name in original_thumbnail_urls)) {
            original_thumbnail_urls[name] = thumbnail.src
        }
    } else {
        if (thumbnail.src.startsWith('data:')) {
            thumbnail.src = original_thumbnail_urls[name]
        }
    }
}
