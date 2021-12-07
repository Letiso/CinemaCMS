const fileInputs = document.getElementsByClassName('form-control-file')

for (let i = 0; i < fileInputs.length; i++) {
    fileInputs[i].setAttribute('onchange', "set_thumbnail(event)")
    // fileInputs[i].addEventListener('change', set_thumbnail)
}

function set_thumbnail(event) {
    const imageInput = event.currentTarget;
    const reader = new FileReader();

    reader.onload = function(){
        image_validation(reader.result, (is_valid) => {
            if (is_valid) {
                const thumbnail = document.getElementById(`${imageInput.id}-thumbnail`);
                thumbnail.src = reader.result;
            }
        })
    };

    reader.readAsDataURL(event.target.files[0]);
  }

function image_validation(src, callback) {
    const image = new Image();

    image.onload = function() {
        console.log(image.naturalWidth, image.naturalHeight);

        if (image.naturalWidth === 1000 && image.naturalHeight === 190) {
            console.log('valid_image');
            callback(true);
        } else {
            console.log('invalid_image');
        }
    }
    image.src = src;
}
