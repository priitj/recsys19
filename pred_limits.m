S = importdata('entropy.tsv','\t',1);
count = importdata('count.tsv','\t',1);
[m, n] = size(S.data);
Pimax = zeros(m,n);

f = @(x,H,M)  H + (x * log2(x) + (1 - x) * log2(1-x)) - (1-x) * log2(M - 1);

for i = 1:n
   for j = 1:m
       tosolve = @(x) f(x, S.data(j, i), count.data(j, i));
       % Pimax(j, i) = S.data(j, i);
       Pimax(j, i) = fzero(tosolve, 0.6);
   end    
end
