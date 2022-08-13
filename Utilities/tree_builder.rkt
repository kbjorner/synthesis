#lang racket

; Collect traces of all paths down tree (unused)
(define tree-trace
  (lambda (tree trace)
    (cond
      ((equal? (car tree) 'ite)
       (append
        (tree-trace
         (car (cdr (cdr tree)))
         (cons (car (cdr tree))
               (cons 'left trace)))
        (tree-trace
         (car (cdr (cdr (cdr tree))))
         (cons (car (cdr tree))
               (cons 'right trace)))))
      (else (cons (reverse trace) '())))))

; Convert list to string
(define create-label
  (lambda (l)
    (string-join (map symbol->string l) " ")))

; Start constructing tree output as s-expression
(define tree-build
  (lambda (tree)
    (cond
      ((equal? (car tree) 'ite)
       `(Tree
         ,(create-label (car (cdr tree)))
         ,(tree-build (car (cdr (cdr tree))))
         ,(tree-build (car (cdr (cdr (cdr tree)))))))
      (else `(Tree ,(create-label tree))))))

; Format s-expression args (inserts ", " between them)
(define sexpr-args-transform
  (lambda (args)
    (cond
      ((null? args) "")
      (else
       (string-append
        (string-append
         (cond
           ((list? (car args)) (sexpr-transform (car args)))
           ((string? (car args)) (string-append "\"" (car args) "\""))
           (else (symbol->string (car args))))
         (if (null? (cdr args)) "" ", "))
        (sexpr-args-transform (cdr args)))))))

; Transform s-expression (the tree notation) into standard form: "func(arg1, arg2)"
(define sexpr-transform
  (lambda (sexpr)
    (cond
      ((null? sexpr) "")
      (else (string-append
             (symbol->string (car sexpr))
             "("
             (sexpr-args-transform (cdr sexpr))
            ")")))))

; Take name of program to convert from standard input
; (file must have been processed with let_unroller.rkt)
(display "File with synthesis output to convert: ")
(define input (call-with-input-file (read-line (current-input-port) 'any) read))

(newline)
(display "Python tree:\n\n")
(display (sexpr-transform (tree-build input)))
(newline)