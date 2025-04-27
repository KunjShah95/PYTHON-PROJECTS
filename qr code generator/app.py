from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    # default colors
    fill_color, back_color = 'black', 'white'

    if request.method == 'POST':
        data = request.form.get('data')
        fill_color = request.form.get('fill_color', 'black')
        back_color = request.form.get('back_color', 'white')
        if data:
            # Create QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            # Save image to memory
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            # Convert to base64
            img_data = base64.b64encode(img_io.getvalue()).decode('ascii')

    return render_template(
        'index.html',
        img_data=img_data,
        fill_color=fill_color,
        back_color=back_color
    )

if __name__ == "__main__":
    app.run(debug=True)
