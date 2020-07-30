%imagesc(A)
colormap(gray)
[m,n] = size(A);
imageSizes = [1,2,4,16,64]

[U, S, V] = svd(A);

%subplot(3,2,1);
%imagesc(A)
%title('Original Image')

for i=1:5
    k = imageSizes(i);
    U_k = U(:,1:k);
    S_k = S(1:k,1:k);
    V_k = V(:,1:k);
    %k rank approximation
    A_new = U_k*S_k*V_k';
    %subplot(3,2,i+1);
    %imagesc(A_new);
    %title(sprintf('Reconstructed Image (k=%d)', int8(imageSizes(i)))); 
end

i = zeros(1,256);
E_k = zeros(1,256);
singularRatio = zeros(1,256);

for k=1:n
    U_k = U(:,1:k);
    S_k = S(1:k,1:k);
    V_k = V(:,1:k);
    
    A_new = U_k*S_k*V_k';
    
    %index
    i(k) = k;
    %error
    E_k(k) = norm(A-A_new)/norm(A);
    %Singular value ratio
    singularRatio(k) = S(k:k,k:k)/S(1:1,1:1);
end

start = 8;

%figure()
scatter(i(1,start:n),E_k(1,start:n),'r')
hold on
scatter(i(1,start:n),singularRatio(1,start:n),'b')
xlabel('k');
ylabel('');
title('Relationship Between Error on Best Rank k Approximation, Singular Value Ratios and k');
legend('Red dot = Error of A_k relative to A','Blue dot = \sigma_k / \sigma_1');
hold off;