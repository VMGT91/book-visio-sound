"""
Script para optimizar imágenes del portfolio
Reduce el tamaño de las imágenes manteniendo buena calidad visual
Requiere: pip install Pillow
"""

from PIL import Image
import os

def optimize_image(input_path, output_path=None, max_width=1920, quality=85):
    """
    Optimiza una imagen reduciéndola y comprimiéndola
    
    Args:
        input_path: ruta de la imagen original
        output_path: ruta de salida (si es None, sobreescribe la original)
        max_width: ancho máximo en píxeles
        quality: calidad de compresión (1-100)
    """
    if output_path is None:
        output_path = input_path
    
    try:
        # Abrir imagen
        img = Image.open(input_path)
        
        # Obtener tamaño original
        original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        print(f"\n📸 Procesando: {os.path.basename(input_path)}")
        print(f"   Tamaño original: {original_size:.2f} MB")
        print(f"   Dimensiones: {img.size[0]}x{img.size[1]} px")
        
        # Redimensionar si es necesario
        if img.size[0] > max_width:
            ratio = max_width / img.size[0]
            new_height = int(img.size[1] * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"   ✂️  Redimensionada a: {max_width}x{new_height} px")
        
        # Convertir RGBA a RGB si es necesario (para JPEG)
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        
        # Determinar formato de salida
        if output_path.lower().endswith('.webp'):
            img.save(output_path, 'WEBP', quality=quality, method=6)
        elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif output_path.lower().endswith('.png'):
            # Convertir PNG a WebP para mejor compresión
            webp_path = output_path.rsplit('.', 1)[0] + '.webp'
            img.save(webp_path, 'WEBP', quality=quality, method=6)
            output_path = webp_path
            print(f"   🔄 Convertido a WebP para mejor compresión")
        
        # Mostrar nuevo tamaño
        new_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"   💾 Tamaño optimizado: {new_size:.2f} MB")
        print(f"   ✅ Reducción: {reduction:.1f}%")
        
    except Exception as e:
        print(f"   ❌ Error procesando {input_path}: {str(e)}")

def main():
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Imágenes a optimizar
    images = [
        'project1.png',
        'project2.png',
        'project6.png',
        'AOT.webp',
        'Cieere Caminos del Vino 2025.webp',
        'Diseño CUM.webp',
        'logo.png'
    ]
    
    print("🚀 Iniciando optimización de imágenes...")
    print("=" * 60)
    
    for img_name in images:
        img_path = os.path.join(current_dir, img_name)
        if os.path.exists(img_path):
            # Guardar backup
            backup_path = os.path.join(current_dir, 'backup_' + img_name)
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(img_path, backup_path)
                print(f"💾 Backup creado: backup_{img_name}")
            
            # Optimizar
            optimize_image(img_path, max_width=1920, quality=85)
        else:
            print(f"\n⚠️  No encontrado: {img_name}")
    
    print("\n" + "=" * 60)
    print("✨ Optimización completada!")
    print("\n📝 NOTA: Se crearon backups con prefijo 'backup_'")
    print("   Si algo sale mal, puedes restaurar los originales.")

if __name__ == "__main__":
    main()
