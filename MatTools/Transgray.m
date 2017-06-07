function [ output ] = Transgray( input )
%Tansfer the 16 bit image to 8 bit image
%   Detailed explanation goes here
    %[m n] = size(input);
    upborder = max(max(input));
    downborder = min(min(input));
    output = (double(input) - double(downborder))*255/(double(upborder) - double(downborder));
    %low_in = double(downborder/65536)
    %high_out = double(upborder/65536)
    %low_out = double(0/65536)
    %high_out = double(255/65536)
    %output = imadjust(double(input), [low_in; high_out], [low_out; high_out]);
    output = uint8(output);
end

