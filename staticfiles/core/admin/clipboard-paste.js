document.addEventListener('paste', function(e) {
    var items = e.clipboardData.items;
    for (var i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
            var blob = items[i].getAsFile();
            var reader = new FileReader();
            reader.onload = function(event) {
                var base64 = event.target.result;
                var input = document.querySelector('input[type="file"][accept*="image"]');
                if (input) {
                    var dt = new DataTransfer();
                    dt.items.add(new File([blob], 'clipboard-image.png', { type: 'image/png' }));
                    input.files = dt.files;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            };
            reader.readAsDataURL(blob);
            break;
        }
    }
});