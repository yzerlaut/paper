import os, sys, subprocess

def export_to_png(svg_filename):
    """
    """
    png_folder = os.path.join(os.path.dirname(svg_filename), 'pngs', 
            os.path.basename(svg_filename).replace('.svg',''))
    if not os.path.isdir(os.path.join(os.path.dirname(svg_filename), 'pngs')):
        os.mkdir(os.path.join(os.path.dirname(svg_filename), 'pngs'))
    if not os.path.isdir(png_folder):
        os.mkdir(png_folder)
    cmd = """
for layer in $(inkscape --query-all %s | grep layer | awk -F, '{print $1}'); do echo "%s -jC -i $layer -e $layer.png"; done
""" % (svg_filename, svg_filename)
    x = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    for c in str(x.stdout).replace('b\'', '').replace('\\n\'', '').split('\\n'):
        os.system('inkscape %s' % c.replace('-e ' , '-e '+png_folder+os.path.sep))

if __name__=='__main__':

    export_to_png(sys.argv[-1])
    #os.system('inkscape templates/slides/drawing-in-inkscape.svg -jC -i layer1 -e layer1.png')

    
    
