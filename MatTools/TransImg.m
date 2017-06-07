%TransImg From 16bit to 8bit
function [img2] = TransImg(name)
    [path, filename, suffix] = fileparts(name)
    suffixlen = length(suffix)
    img = imread(name);
    [m n z] = size(img);
    if z == 1
        img2 = Transgray(img);
    end
    if z == 3
        img2 = Transrgb(img);
    end
    %dir = ['img8\' name(1:length(name) - suffixlen) '.tiff'];
    %imwrite(img2, dir);
end