const fileInputs = document.getElementsByClassName('form-control-file')

for (let i = 0; i < fileInputs.length; i++) {
    fileInputs[i].setAttribute('onchange', "set_thumbnail(event)")
}

function set_thumbnail(event) {
    const imageInput = event.currentTarget

    const reader = new FileReader();
    reader.onload = function(){
        const thumbnail = document.getElementById(`${imageInput.getAttribute('id')}-thumbnail`)
        thumbnail.src = reader.result;
    };

    reader.readAsDataURL(event.target.files[0]);
  }
