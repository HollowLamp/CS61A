(define (split-at lst n)
  (if (or (null? lst) (<= n 0))
      (cons '() lst)
      (let ((result (split-at (cdr lst) (- n 1))))
        (cons (cons (car lst) (car result)) (cdr result)))))



(define (compose-all funcs)
  (if (null? funcs)
      (lambda (x) x)
      (lambda (x)
        ((compose-all (cdr funcs)) ((car funcs) x)))))

