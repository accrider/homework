(defun palindrome(lst)
	(if (< (length lst) 2)
		t
		(if (equal (car lst) (car (reverse lst))) 
			(palindrome (cdr (reverse (cdr (reverse lst)))))
			nil)))


(defun palindrome-filter (f lst)
	(cond ((not lst) nil)
	(t (cons (funcall f (car lst)) (palindrome-filter f (cdr lst)) ))))

(defun addxtopowerset(x pset)
	(if (null pset)
		(list nil)
	(remove-duplicates (append (cons (cons x (car pset))
	(addxtopowerset x (cdr pset))) pset))))

(defun powerset(lst) 
	(if (null lst) (list nil)
	(addxtopowerset (car lst) (powerset(cdr lst)))))