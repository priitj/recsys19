% calculate Pi^max (predictability with perfect algo)
% from entropy estimate S, with number of distinct elements
% in sequence m
%S = 7.136608275066677;
S = 10.1952677
%m = 32053;
m = 91053;
f = @(x)  S + (x * log2(x) + (1 - x) * log2(1-x)) - (1-x) * log2(m - 1);
x = fzero(f, 0.5)
