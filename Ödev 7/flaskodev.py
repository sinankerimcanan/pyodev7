from flask import Flask, render_template_string, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask Uygulaması</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
            }
            header {
                position: absolute;
                top: 0;
                right: 0;
                margin: 20px;
            }
            .name {
                color: white;
                margin-right: 10px; /* Boşluk eklemek için */
            }
            .id {
                color: white;
            }
            .button {
                display: block;
                margin: 100px auto;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: darkmagenta;
                border: none;
                cursor: pointer;
                text-align: center;
            }
            .button:hover {
                background-color: purple;
            }
        </style>
    </head>
    <body>
        <header>
            <h1><span class="name">Sinan Kerim Canan </span><span class="id">211213004</span></h1>
        </header>
        <main>
            <button class="button" onclick="generateImage()">Görsel Oluştur</button>
            <div id="image-container"></div>
        </main>
        <script>
            function generateImage() {
                fetch('/generate-image')
                .then(response => response.blob())
                .then(blob => {
                    var url = URL.createObjectURL(blob);
                    var img = document.createElement('img');
                    img.src = url;
                    img.style.display = 'block';
                    img.style.margin = '20px auto';
                    document.getElementById('image-container').innerHTML = '';
                    document.getElementById('image-container').appendChild(img);
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/generate-image')
def generate_image():
    num_points = 1000  
    x_coords = np.random.randint(0, 1001, num_points)  
    y_coords = np.random.randint(0, 1001, num_points)  
    
    df = pd.DataFrame({'X': x_coords, 'Y': y_coords})  # veri çerçevesi
    
    
    df.to_excel('koordinatlar.xlsx', index=False) 
    
    
    plt.figure(figsize=(8, 8)) 
    
    grid_size = 200  # Alt ızgara boyutunu
    num_grids = int(1000 / grid_size)  # Toplam alt ızgara sayısı
    colors = np.random.rand(num_grids ** 2, 3)  # rastgele renk
    color_index = 0
    for i in range(0, 1001, grid_size): #x
        for j in range(0, 1001, grid_size): #y
            x_in_grid = df[(df['X'] >= i) & (df['X'] < i + grid_size)]  # X koordinatı içinde olan noktalar
            y_in_grid = x_in_grid[(x_in_grid['Y'] >= j) & (x_in_grid['Y'] < j + grid_size)]  # Y koordinatı içinde olan noktalar
    
    
            if not y_in_grid.empty:  # ızgara içinde nokta varsa 
                color = colors[color_index % (num_grids ** 2)]  # renk belirler.
                plt.scatter(y_in_grid['X'], y_in_grid['Y'], s=5, c=[color] * len(y_in_grid), alpha=0.5)  # noktaları renklendirerek çizer.
                color_index += 1  # Renk indeksini artırır.

    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.title('Rastgele Noktaların Görselleştirilmesi')

    # Görseli belleğe kaydet
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
