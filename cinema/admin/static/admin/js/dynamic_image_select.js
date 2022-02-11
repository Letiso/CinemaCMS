// init original_thumbnail_urls var for thumbnails img.src backup
const original_thumbnail_urls = {}


// TODO * PAY ATTENTION * you have to define something like that at the template
//  <script>
//      const required_sizes = {
//          '{{ your_form.prefix }}': ['{{ required_size.0 }}', '{{ required_size.1 }}'],
//      }
//  <script>
//   because we need to take data from view context for dynamic validation


// Event listener binding for bootstrapped file inputs
const fileInputs = document.getElementsByClassName('form-control-file')

for (let i = 0; i < fileInputs.length; i++) {
    fileInputs[i].setAttribute('onchange', 'validate_then_set_thumbnail(event)')
}
// end of Event listener binding

function validate_then_set_thumbnail(event) {
    const imageInput = event.currentTarget;
    const reader = new FileReader();

    reader.onload = function() {
        const fileInputData = imageInput.name.split('-');
        const form_prefix = fileInputData[0];
        const field_name = fileInputData[fileInputData.length - 1];

        const required_size = required_sizes[form_prefix][field_name];

        image_validation(reader.result, required_size, (is_valid) => {
            const thumbnail = document.getElementById(`${imageInput.id}-thumbnail`);

            if (is_valid) {
                original_thumb_url_backup(imageInput.name, thumbnail);
                thumbnail.src = reader.result;
                toggle_error(true, imageInput, required_size);

                toastr.success('Данные валидны');
            } else {
                original_thumb_url_backup(imageInput.name, thumbnail, true);
                toggle_error(false, imageInput, required_size);

                toastr.error('Данные невалидны');
            }
        })
    };

    reader.readAsDataURL(event.target.files[0]);
  }


function image_validation(src, required_size, callback) {
    const image = new Image();

    image.onload = function() {
        console.log([image.naturalWidth, image.naturalHeight])
        console.log(required_size)
        if (JSON.stringify([image.naturalWidth, image.naturalHeight]) === JSON.stringify(required_size)) {
            callback(true);
        } else {
            callback(false);
        }
    }
    // image.onload event type
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
