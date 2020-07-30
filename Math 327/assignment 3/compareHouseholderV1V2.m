function [expTimes, imTimes] = compareHouseholderV1V2(n)

expTimes = zeros(1,10);
imTimes = zeros(1,10);

for k = 1:n
    A =randn (100 * k, 50 * k);
    %Explicit Method
    tic;
    HouseHolder(A);
    expTimes(k) = toc;
    %Implicit Method
    tic;
    HouseHolderIm(A);
    imTimes(k) = toc;
end