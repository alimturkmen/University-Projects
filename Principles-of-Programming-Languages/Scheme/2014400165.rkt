#lang scheme
; compiling: yes
; complete: yes
; 2014400165
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.1
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (card-color one-card) -> string?
; one-card : pair?

; Looks the first item of the pair.
; If the head is H or D returns red, otherwise returns black.

; Example:
; > (card-color '(C . 10)
; => black
(define (card-color one-card)
  (cond
   [(equal? (car one-card) 'H) 'red]
   [(equal? (car one-card) 'D) 'red]
   [else 'black]
   )
  )

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.2
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (card-rank one-card) -> number?
; one-card : pair?

; Looks the second item in the pair.
; If it is A returns 11,
; if it is Q or K or J returns 10,
; otherwise returns the second item.

; Example:
; > (card-rank '(C . A)
; => 11
(define (card-rank one-card)
  (cond
    [(equal? (cdr one-card) 'A) '11]
    [(equal? (cdr one-card) 'Q) '10]
    [(equal? (cdr one-card) 'K) '10]
    [(equal? (cdr one-card) 'J) '10]
    [else (cdr one-card)]
    )
  )
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.3
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (all-colors list-of-cards) -> list?
; list-of-cards : list?

; Takes a list and returns the colors of the cards in this list.
; To determine the card color uses the first function.

; Example:
; > (all-colors '((C . 10) (H . 5) (D . 2))
; => (black red red)
(define (all-colors list-of-cards)
  (map card-color list-of-cards))

; (all-same-color list-of-cards) -> boolean?
; list-of-cards : list?

; Checks whether all the cards in a list have the same color or not.
; Looks if the card list contains both of the colors.
; If it does returns false, for other cases returns true.

; Example:
; > (all-same-color '((C . 10) (H . 5) (D . 2))
; => #f
(define (all-same-color list-of-cards)
 (not (and (member 'black (all-colors list-of-cards)) (member 'red (all-colors list-of-cards))) ))
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.4
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (fdraw list-of-cards held-cards) -> list?
; list-of-cards : list?
; held-cards : list?

; Takes the first element in the card list, makes it a list with an element
;and appends it to the held cards.

; Example:
; > (fdraw '((H . 3) (H . 2) (H . A) (D . A) (D . Q) (D . J)) '((S . 3) (S . 2) (S . A)))
; => ((S . 3) (S . 2) (S . A) (H . 3))
(define (fdraw list-of-cards held-cards)
 (append held-cards (list (car list-of-cards)))
  )

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.5
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (min-of-alist alist acard) -> pair?
; alist : list?
; acard : pair?

; Finds the card with lowest card-rank in a given list.
; If there is more than one card with lowest card-rank returns the
; one that is encountered first.

; Example:
; > (min-of-alist '((H . 10) (H . 5) (D . 2) (C . 2)) '(H . 10))
; => (D . 2)
(define (min-of-alist alist acard)
  (cond
   [(null? alist) acard]
   [(< (card-rank (car alist)) (card-rank acard) ) (min-of-alist (cdr alist) (car alist))]
   [else (min-of-alist (cdr alist) acard)]
   )
  )
; (fdiscard list-of-cards list-of-moves goal held-cards) -> list?
; list-of-cards : list?
; list-of-moves : list?
; goal : number?
; held-cards : list?

; Discards the card with lowest card-rank.
; In other words removes the card with lowest card-rank from the held-cars.

; Example:
; > (fdiscard '() '() 0 '((H . 10) (C . 8) (D. 1)))
; => ((H . 10) (C . 8))
(define (fdiscard list-of-cards list-of-moves goal held-cards)
 (remove (min-of-alist held-cards (car held-cards)) held-cards ))
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.6
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (find-step-with-held-cards list-of-cards held-cards list-of-moves) -> list?
; list-of-cards : list?
; held-cards : list?
; list-of-moves : list?

; Takes list-of-cards, held-cards and list-of-moves and returns the list of steps.
; It is a recursive function.
; It has three terminating conditions:
; 1 Emptiness of the list-of-moves
; 2 If the following move is "draw", emptiness of list-of-cards
; 3 If the following move is "discard" emptiness of the held-cards
; For terminating conditions it returns an empty list.
; In other cases takes the list-of-moves's first element, if it is "draw" takes the
;first card in list-of-cards, otherwise takes the card with lowest card-rank from
;held-cards and creates a list. (Since I didn't use list-of-cards, list-of-moves
;and goal in fdiscard(see part 4.5), I send empty lists for lists and 0 for goal)
; Appends the created list to the list that will be created for the rest of
;list-of-moves, held-cards and list-of-cards.

; Example:
; > (find-steps-with-held-cards '((H . 5) (H . 2)) '() '(draw draw discard))
; => ((draw (H . 5)) (draw (H . 2)) (discard (H . 2)))
(define (find-steps-with-held-cards list-of-cards held-cards list-of-moves)
  (cond
    [(null? list-of-moves) '()]
    [(equal? (car list-of-moves) 'draw) (if (null? list-of-cards) '()
     (append
      (list (list 'draw (car list-of-cards)))
      (find-steps-with-held-cards (cdr list-of-cards) (fdraw list-of-cards held-cards) (cdr list-of-moves) )))]
    [else (if (null? held-cards) '()
     (append
      (list (list 'discard (min-of-alist held-cards (car held-cards))))
      (find-steps-with-held-cards list-of-cards  (fdiscard '() '() 0 held-cards) (cdr list-of-moves) )))]
    )
  )
; (check-for-goal step-list score goal) -> list?
; step-list : list?
; score : number?
; goal : number?

; Since the game should be ended if playerpoint is greater than goal,
;I should cut the list whenever playerpoint is greater than goal.
;(playerpoint : sum of card-ranks in held-cards)
; Again it is a recursive function
; It takes the steps from the step list until either the step-list empty or
;score gets greater than goal.
; In order to calculate the score, if the step is "draw" adds card-rank to the score
;if the step is "discard" subtracts card-rank from the score.

; Example:
; > (check-for-goal '((draw (H . 2)) (draw (H . A)) (discard (H . 2)) (draw (H . 10)) (discard (H . 10))) 0 15)
; => ((draw (H . 2)) (draw (H . A)) (discard (H . 2)) (draw (H . 10)))
(define (check-for-goal step-list score goal)
  (cond
    [(null? step-list) '()]
    [(> score goal) '()]
    [(equal? (car (car step-list)) 'draw)
     (append
      (list (car step-list))
      (check-for-goal (cdr step-list) (+ score (card-rank (car (cdr (car step-list))))) goal))]
    [else
     (append
      (list (car step-list))
      (check-for-goal (cdr step-list) (- score (card-rank (car (cdr (car step-list))))) goal))]
    )
  )
; (find-steps list-of-cards list-of-moves goal) -> list?
; list-of-cards : list?
; list-of-moves : list?
; goal : number?

; Uses the 2 functions above. First, finds the all steps by using "find-steps-with-held-cards"
;then checks the returned list for goal. Since, there is no card in held-cards at the beginning
;sends an empty list for held-cards and 0 for score.

; Example:
; > (find-steps '((H . 5) (H . 2)) '(draw draw discard) 6)
; => ((draw (H . 5)) (draw (H . 2)))
(define (find-steps list-of-cards list-of-moves goal)
 (check-for-goal (find-steps-with-held-cards list-of-cards '() list-of-moves) 0 goal ))
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.7
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (find-held-cards-with-held-cards list-of-steps held-cards) -> list?
; list-of-steps : list?
; held-cards : list?

; It is a recursive function.
; The terminating condition is emptiness of list-of-steps.
;In terminating condition returns held cards.
; Creates held-cards with a given list-of-steps.
; Initially held-cards is empty. For each step, if it is "draw"
;adds the card in the step to held-cards, if it is "discard"
;removes the card in the step from held-cards.
; For "draw" step, appends current held-cards to the new card and
;and sends new held-cards to the same function
; For "discard" step, removes the card from held-cards and sends
;new held cards to the same function
; Same processes keep going until the terminating condition.

; Example:
; > ( find-held-cards '((draw (H . 3)) (draw (H . 2)) (draw (H . A)) (discard (H . 3))) )
; => ((H . 2) (H . A))
(define (find-held-cards-with-held-cards list-of-steps held-cards)
(cond
 [(null? list-of-steps) held-cards]
  [(equal? (car (car list-of-steps)) 'draw)
   (find-held-cards-with-held-cards
    (cdr list-of-steps)
    (append held-cards (cdr (car list-of-steps)) )
    )]
  [else
  (find-held-cards-with-held-cards
   (cdr list-of-steps)
   (remove (car (cdr (car list-of-steps))) held-cards)
   )]
  )
  )
; (find-held-cards list-of-steps) -> list?
; list-of-steps : list?

; I thought recursively for this function like all of the functions above.
; For "discard" steps, we have to access the list we have created till
;that step. Hence, I used find-held-cards-with-held-cards.
(define (find-held-cards list-of-steps)
  (find-held-cards-with-held-cards list-of-steps '())
 )

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.8
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (calc-playerpoint list-of-cards) -> number?
; list-of-cards : list?

; Calculates the sum of card-ranks of the cards in held-card.
; It is a recursive function.
; Until it reaches the end of the list-card, adds card-ranks of cards
; to playerpoint.

; Example:
; > ( calc-playerpoint '((H . A) (H . 3) (H . 2) (D . Q) (D . J) (C . J)) )
; => 46
(define (calc-playerpoint list-of-cards)
  (if (null? list-of-cards) 0 (+ (card-rank (car list-of-cards)) (calc-playerpoint (cdr list-of-cards)))))

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.9
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (calc-prescore list-of-cards goal) -> number?
; list-of-cards : list?
; goal : number?

; Calculates prescore of held-cards. If playerpoint is greater than goal
;subtracts goal from playerpoint and multiplies the result by 5, otherwise just
;subtracts playerpoint from goal.
; To calculate playerpoint uses the function in part 4.8

; > (calc-prescore '((H . 2) (H . A)) 10)
; => 15
(define (calc-prescore list-of-cards goal)
  (if (> (calc-playerpoint list-of-cards) goal) (* 5 (- (calc-playerpoint list-of-cards) goal))
       (- goal (calc-playerpoint list-of-cards))))
; (calc-score list-of-cards goal) -> number?
; list-of-cards : list?
; goal : number?

; Calculates the final score which equals to half of the prescore if
;all of the cards in held-card have same color (rounded down with integer division),
;otherwise just equals to prescore.

; Example:
; > ( calc-score '((H . 3) (H . 2) (H . A) (D . J) (D . Q) (C . J)) 16 )
; => 150
(define (calc-score list-of-cards goal)
  (if (all-same-color list-of-cards) (floor (/ (calc-prescore list-of-cards goal) 2)) (floor (calc-prescore list-of-cards goal))))

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;                         4.10
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; (play list-of-cards list-of-moves goal) -> number?
; list-of-cards : list?
; list-of-moves : list?
; goal : number?

; Briefly plays the game.
; It has three steps:
; Firstly, creates the list of the steps by using find-steps,
; Secondly using the list-of-steps creates held-card
; Finally calculates the score using held-card

; Example:
; > (play '((C . 3) (C . 2) (C . A) (S . J) (S . Q) (H . J))
;     '(draw draw discard discard discard discard discard draw) 14)
; => 7
(define (play list-of-cards list-of-moves goal)
  (calc-score (find-held-cards (find-steps list-of-cards list-of-moves goal)) goal))

