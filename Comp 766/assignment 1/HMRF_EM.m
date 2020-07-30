%%  The EM algorithm

function [X mu sigma]=HMRF_EM(Y,mu,sigma,k,EM_iter,pi_ki)
%dimensions of image
[m, n]=size(Y);

%flatten gaussian blurred image
y=Y(:);

%prob likelihood of y_i (observed pixel value) being in each class
P_lyi=zeros(k,m*n);

%alpha vector
alpha = ones(1,m*n)*0.01;

for it=1:EM_iter
    fprintf('Iteration: %d\n',it);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Biological Constraint 3 
    beta = 0.1;
    n_i=zeros(1,m*n);
    alphaCopy = alpha;
    alphaShape=reshape(alphaCopy,[m n]);
    %neighbour calculation for biological constraint
    for ind=1:m*n
        [i j]=ind2ij(ind,m);
        soft=0;
        if i-1>=1
            soft=soft + alphaShape(i-1,j);
        end
        if i+1<=m
            soft=soft + alphaShape(i+1,j);
        end
        if j-1>=1
            soft=soft + alphaShape(i,j-1);
        end
        if j+1<=n
            soft=soft + alphaShape(i,j+1);
        end
        n_i(1,ind) = soft;
    end
    phi = alpha./ (alpha + ((1-alpha) .* exp(-beta*(2*n_i - 6))));
    
    %E-step%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    S = zeros(2*k,m*n);
    %Equation 9
    for t_i=0:1 % iterate over t_i
        for k_i=1:(k-1)
            %index goes from 0 to 2(k-1)
            index = (t_i*(k-1)) + k_i;
            
            %prior estimation of pixel i from the 'atlas'
            temp1 = pi_ki(k_i,:);
            %t_1 = 0 => tissue label vector would be k_i (Healthy tissue)
            if t_i == 0
                %compute Normal with mu and sigma of healthy tissue class
                %k_i
                S(index,:) = temp1 .* (1-phi).*transpose((1/sqrt(2*pi*sigma(k_i)^2)*exp(-(y-mu(k_i)).^2/2/sigma(k_i)^2)));
                %C = temp1 .* (1-alpha);
                %N = transpose((1/sqrt(2*pi*sigma(k_i)^2)*exp(-(y-mu(k_i)).^2/2/sigma(k_i)^2)));
            %t_1 = 1 => tissue label vector would be k (Tumor)
            else
                %compute Normal with mu and sigma of Tumor class (i.e.
                %class k)
                S(index,:) = temp1 .* (phi).* transpose((1/sqrt(2*pi*sigma(k)^2)*exp(-(y-mu(k)).^2/2/sigma(k)^2)));
            end
        end
    end
    %normalize
    temp3=sum(S,1);
    S=bsxfun(@rdivide,S,temp3);
    
    %Equation 10
    temp2 = zeros(1,m*n);
    %sum over bottom k-1 rows of S
    for k_i=k:(2*(k-1))
        temp2 = temp2 + S(k_i,:);
    end
    %k-th row of P_lyi is for Tumor class
    P_lyi(k,:) = temp2;
    
    %Equation 11
    %Just take the row
    for k_i=1:(k-1)
        %rows 1 to k-1 are for healthy tissue classes
        P_lyi(k_i,:) = S(k_i,:);
    end
    
    
    %M-Step%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Equation 12
    %C = 1, since we only have one channel
    %drop normalization constant and summation
    alpha(:) = P_lyi(k,:);
    
    % get mu and sigma
    % Equations 13/15 and 14/16 from paper 
    % k-1 healthy tissue classes, 1 tumour class
    for l=1:k % all labels
        mu(l)=P_lyi(l,:)*y;
        mu(l)=mu(l)/sum(P_lyi(l,:));
        sigma(l)=P_lyi(l,:) * ( (y-mu(l)).^2 );
        sigma(l)=sigma(l)/sum(P_lyi(l,:));
        sigma(l)=sqrt(sigma(l));
    end
    
%compute class labels here
%class label for each pixel is just the most likely class according to the
%calculate probability distribution for each pixel
[M,I] = max(P_lyi,[],1);

X=reshape(I,[m n]);
imwrite(uint8(X*70),'iteration labels.png');    
    
end