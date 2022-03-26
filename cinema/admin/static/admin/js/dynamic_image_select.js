// init original_thumbnail_urls var for thumbnails img.src backup
const original_thumbnail_urls = {}


// REQUIRED_SIZES structure is a simple:

//  REQUIRED_SIZES = {
//      'form_prefix_1': {
//         'field_name_1': [width, height],
//         'field_name_2': [1920, 1080],
//         ...
//      },
//      'form_prefix_2': {
//          ...
//      },
//      ...


// TODO * PAY ATTENTION * you have to define:
//  <script>
//      const REQUIRED_SIZES = JSON.parse('{{ required_sizes|safe }}')
//  initRequiredSizeLabels()
//  <script>
//  (you just can copy the code below and paste it at your template)

//   because we need to take data from django's context to js for dynamic validation


// actually, required sizes labels init
function initRequiredSizeLabels() {
    for (const [form_prefix, form_required_sizes] of Object.entries(REQUIRED_SIZES)) {
        for (const [field_name, required_size] of Object.entries(form_required_sizes)) {
            // this way we can get *form_prefix, field_name* strings
            // and *required_size* array

            // also, you have to set id for every required_size_label looking like:
            // <tag id="form_prefix-field_name-required_size">
            let required_size_label = $(
                `*[id*="${form_prefix}"][id*="${field_name}"][id$="-required_size"]`
            )
            required_size_label.html(`${gettext('Size')} ${required_size[0]}x${required_size[1]}`)
        }
    }
}


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

        const required_size = REQUIRED_SIZES[form_prefix][field_name];

        image_validation(reader.result, required_size, (is_valid) => {
            const thumbnail = document.getElementById(`${imageInput.id}-thumbnail`);

            if (is_valid) {
                original_thumb_url_backup(imageInput.name, thumbnail);
                thumbnail.src = reader.result;
                toggle_error_message(true, imageInput, required_size);

                toastr.success(gettext('Data is valid'));
            } else {
                original_thumb_url_backup(imageInput.name, thumbnail, true);
                toggle_error_message(false, imageInput, required_size);

                toastr.error(gettext('Invalid data'));
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
    // image.onload event type
    image.src = src;
}


function toggle_error_message(validation_succeed, imageInput, required_size) {
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
            p.innerHTML = `<strong>${gettext('Select image with next resolution')}: ${required_size[0]}x${required_size[1]}</strong>`;

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
