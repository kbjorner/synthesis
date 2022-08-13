#lang racket
(require fmt)

; Strips away the "Bool"s and "let"s wrapping the program, down to the first "ite"
(define strip
  (lambda (prog)
    (cond
      ((null? prog) '())
      ((equal? (car prog) 'Bool) (strip (car (cdr prog))))
      ((equal? (car prog) 'let) (strip (car (cdr (cdr prog)))))
      (else prog))))

; Collects the let expressions (variable substitutions) into a map
(define collect
  (lambda (prog)
    (cond
      ((equal? (car prog) 'Bool) (collect (car (cdr prog))))
      ((equal? (car prog) 'let)
       (cons (car (car (cdr prog)))
             (collect (car (cdr (cdr prog))))))
      (else '()))))

; Query a map with a key (returns false if not found)
(define get
  (lambda (map key)
    (cond
      ((null? map) #f)
      ((equal? (car (car map)) key) (car (cdr (car map))))
      (else (get (cdr map) key)))))

; Replace every occurence of map keys in a list with their corresponding values
(define insert
  (lambda (prog map)
    (cond
      ((null? prog) '())
      ((list? prog) (cons (insert (car prog) map) (insert (cdr prog) map)))
      (else (let ((value (get map prog)))
              (if value value prog))))))

; Take program name from standard input
(display "File to convert: ")
(define input (call-with-input-file (read-line (current-input-port) 'any) read))

; Process program
(define substitutions (collect input))
(define unrolled (insert (strip input) substitutions))

; Print all substitutions
(printf "\nFound ~s let expressions:\n" (length substitutions))
(for [(x substitutions)]
  (printf "~s -> ~s\n" (car x) (car (cdr x))))

; Create output file
(display "\nFile to generate: ")
(call-with-output-file (read-line)
  (lambda (out)
    (display (program-format (~a unrolled)) out))
  #:exists 'replace
  #:mode 'text)