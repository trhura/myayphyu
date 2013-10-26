#! /usr/bin/ruby

require "csv"
require "pango"
require "cairo"

WIDTH=800
HEIGHT=600

def main
    ARGV.each do |arg|
        if not FileTest.exist? arg
            puts "#{arg} doesn't exist."
            next
        end

        filename = File.basename arg, File.extname(arg)
        markup = File.read arg
        puts "Generating image for #{arg}"

        # surface
        surface = Cairo::ImageSurface.new Cairo::FORMAT_ARGB32, WIDTH , HEIGHT
        context = Cairo::Context.new surface

        # white transparent background
        context.set_source_rgba 1, 1, 1, 0.0
        context.paint

        # Layout
        layout = context.create_pango_layout
        layout.width = WIDTH * Pango::SCALE
        layout.markup = markup

        # show text
        context.set_source_color (:black)
        context.update_pango_layout layout
        context.show_pango_layout layout

        # write to image
        surface.write_to_png(filename + ".png")
    end
end

main
