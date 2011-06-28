import sys
import gtk
import webkit

class OutputView(webkit.WebView):

    def __init__(self, dst):
        webkit.WebView.__init__(self)
        self.dst = dst
        self.connect("load-finished", self.on_load_finished)

    def on_load_finished(self, webview, webframe):
        root = self.get_parent_window()
        rect = self.get_allocation()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, rect.width, rect.height)
        pixbuf.get_from_drawable(root, root.get_colormap(), rect.x, rect.y, rect.x, rect.y, rect.width, rect.height)
        pixbuf.save(self.dst, "png", {})
        gtk.main_quit()


class Window(gtk.Window):

    def __init__(self, output):
        gtk.Window.__init__(self)
        self.set_default_size(1024, 768)
        self.scroll = gtk.ScrolledWindow()
        self.output = output
        self.scroll.add(self.output)
        self.add(self.scroll)
        self.scroll.show_all()

    def load(self, url):
        self.output.load_uri(url)


window = Window(OutputView(sys.argv[2]))
window.load(sys.argv[1])
window.show()
gtk.main()
