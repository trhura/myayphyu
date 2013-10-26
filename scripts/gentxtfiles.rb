#! /usr/bin/env ruby

(0x1000..0x1026).each do |x|
    utf8char =  [x].pack('U')
    filename = x.to_s
    File.open(filename + ".txt", "w") do |file|
        file.write(utf8char)
    end
end
