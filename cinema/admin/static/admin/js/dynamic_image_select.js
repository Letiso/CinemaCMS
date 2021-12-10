// init original_thumbnail_urls var
const original_thumbnail_urls = {}


// kind of event listener for file inputs
const fileInputs = document.getElementsByClassName('form-control-file')

for (let i = 0; i < fileInputs.length; i++) {
    fileInputs[i].setAttribute('onchange', "validate_then_set_thumbnail(event)")
}


function validate_then_set_thumbnail(event) {
    toastr.info('Был выбран файл');

    const imageInput = event.currentTarget;
    const reader = new FileReader();

    reader.onload = function() {
        const required_size = document.getElementById(
            imageInput.name.split('-')[0]).getElementsByClassName(
                'required-size')[0].innerHTML.split('x')

        image_validation(reader.result, required_size, (is_valid) => {
            const thumbnail = document.getElementById(`${imageInput.id}-thumbnail`);

            if (is_valid) {
                original_thumb_url_backup(imageInput.name, thumbnail.src)
                thumbnail.src = reader.result;
                toggle_error(true, imageInput, required_size)
            } else {
                thumbnail.src = original_thumb_url_backup(imageInput.name, false)
                toggle_error(false, imageInput, required_size)
            }
        })
    };

    reader.readAsDataURL(event.target.files[0]);
  }


function image_validation(src, required_size, callback) {
    const image = new Image();

    image.onload = function() {
        if (JSON.stringify(['' + image.naturalWidth, '' + image.naturalHeight]) === JSON.stringify(required_size)) {
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


function original_thumb_url_backup(name, src) {
    if (src && !(name in original_thumbnail_urls)) {
        original_thumbnail_urls[name] = src
    } else {
        return original_thumbnail_urls[name]
    }
}
