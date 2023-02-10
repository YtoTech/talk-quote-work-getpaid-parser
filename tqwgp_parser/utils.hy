; (require [hy.extra.anaphoric [ap-each]])

(import copy)
(import toolz.itertoolz [drop])
(require hyrule [assoc])

; Predicates.

(defn numeric? [v]
  (isinstance v (, int float)))

(defn string? [v]
  (isinstance v (, str bytes)))

(defn none? [v]
  (= v None))

(defn none-or-true? [value]
  (or (none? value) (bool value)))


; Dicts.

(defn parse-dict-values [value mandatories optionals]
  ;; Use dict-comp http://docs.hylang.org/en/stable/language/api.html#dict-comp?
  (setv parsed-dict {})
  (for [key (.keys value)] ((fn [key]
    (if (or (in key mandatories) (in key optionals))
      (assoc parsed-dict key (get value key))
      (print (.format "Ignoring key {}" key)))) key))
  ;; Check all mandatories are here.
  (for [mandatory mandatories] ((fn [mandatory]
    (if (not (in mandatory parsed-dict))
      (raise (ValueError (.format "Missing key {}" mandatory))))) mandatory))
  ;; Affect None to non-set optionals.
  (for [optional optionals] ((fn [optional]
    (if (not (in optional parsed-dict))
      (assoc parsed-dict optional None))) optional))
  parsed-dict)

(defn merge-dicts [dicts]
  (setv merged (.deepcopy copy (get dicts 0)))
  (for [one-dict (drop 1 dicts)] ((fn [one-dict]
    (.update merged one-dict)) one-dict))
  merged)

; (defn filter-dict [a-dict pred]
;   (setv new-dict {})
;   (ap-each (.keys a-dict)
;     (if (pred (get a-dict it) it)
;       (assoc new-dict it (get a-dict it))))
;   new-dict)
(defn filter-dict [a-dict pred]
  (setv new-dict {})
  (for [key (.keys a-dict)]
    ((fn [key]
      (if (pred (get a-dict key) key)
        (assoc new-dict key (get a-dict key))))
      key))
  new-dict)

(defn pick-by [pred value]
  (setv new-value {})
  (for [key (.keys value)] ((fn [key]
    (if (pred key)
      (assoc new-value key (get value key)))) key))
  new-value)

(defn get-default [value key default]
  (if (in key value)
    (get value key)
    default))

(defn get-in [value key-path default]
  (setv current-key (if (= (len key-path) 0) None (get key-path 0)))
  (if (none? current-key)
    default
    (if (in current-key value)
      (if (= (len key-path) 1)
        (get value current-key)
        (get-in
          (get value current-key)
          (cut key-path 1 None)
          default))
      default)))

; Lists.

(defn find-in-list [l pred]
  (setv element None)
  (for [item l] ((fn [item])
    (if (pred item)
      (do
        (setv element item)
        (break))) l))
  element)


; Numbers.

(defn simplest-numerical-format [price]
  (if (.is_integer (float price))
    (int price)
    price))

(defn rounded-number [number-value rounding-decimals]
  (print number-value rounding-decimals)
  (if (and number-value rounding-decimals)
    (round number-value rounding-decimals)
    number-value))

; Misc.

