clear;clc;close all;

%number of tissue classes specified in question
k = 4;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Atlas photo
I=imread('input_image_atlas_prior.PNG');
Y=rgb2gray(I);
Y=double(Y);
Y=gaussianBlur(Y,3);
imwrite(uint8(Y),'blurred image prior.png');

%perform (k-1) means using the atlas photo to compute our priors
fprintf('Performing k-means segmentation\n');
[X_prior, mu_prior, sigma_prior]=image_kmeans(Y,k-1);
imwrite(uint8(X_prior*60),'initial labels prior.png');

%Equation 1
%pi distribution (prior)
[m, n]=size(Y);

%k=3 case, pi can be initialized without smoothing
%this results in a binary distribution at each pixel i
%since we only had one prior image
if k == 3
    pi_ki = zeros(k-1,m*n);
    for ind=1:m*n
        [i,j]=ind2ij(ind,m);
        class = X_prior(i,j);
        pi_ki(class,ind) = 1;
    end
%k=4 case requires smoothing because kmeans does not get a good initial
%estimation of which pixels belong to which class, specifically the tumor
%border class
else
    pi_ki = ones(k-1,m*n)*(1/4); 
    for ind=1:m*n
        [i,j]=ind2ij(ind,m);
        class = X_prior(i,j);
        pi_ki(class,ind) = 1/2;
    end
end

healthy_prior = X_prior(25,185) %should be healthy tissue
background_prior = X_prior(200,20) %should be background
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Tumor photo

I=imread('input_image_tumor.PNG');
Y=rgb2gray(I);
Y=double(Y);
Y=gaussianBlur(Y,3);
imwrite(uint8(Y),'blurred image.png');

EM_iter=30; % max num of iterations

tic;
fprintf('Performing k-means segmentation\n');
[X, mu, sigma]=image_kmeans(Y,k);
imwrite(uint8(X*60),'initial labels.png');


mu = [120,120,120,120]
sigma = [15,15,15,15]

%This code makes sure that the intial estimates for the tumor class are in
%index k of each parameter (since this is what the model assumes)
%value that kmeans has given to the tumor segment
tumor = X(110,80);
%get tumor pixels = k
%get mu and sigma for tumor to end of the list
X(X==tumor)=10;
X(X==k)=tumor;
X(X==10)=k;
tempMu = mu(tumor);
tempSigma = sigma(tumor);
mu(tumor) = mu(k);
sigma(tumor) = sigma(k);
mu(k) = tempMu;
sigma(k) = tempSigma;


healthy = X(25,185) %should be healthy tissue
background = X(200,20) %should be background

%note for successful test:
%healthy_prior = healthy and background_prior = background required
%otherwise the prior distribution pi is representing the wrong class
%this issue is created by kmeans since the ordering of classes is non
%deterministic in kmeans

[X, mu, sigma]=HMRF_EM(Y,mu,sigma,k,EM_iter,pi_ki);
imwrite(uint8(X*60),'final labels.png');
toc;