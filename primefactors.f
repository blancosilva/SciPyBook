C FILE: PRIMEFACTORS.F
	SUBROUTINE PRIMEFACTORS(num, factors, f)
	IMPLICIT NONE
	INTEGER, INTENT(IN) :: num  
	INTEGER,INTENT(OUT), DIMENSION((num/2))::factors 
	INTEGER, INTENT(INOUT) :: f
	INTEGER :: i, n
Cf2py	intent(in) num
Cf2py	intent(out) factors
Cf2py	depend(num) factors
	i = 2  
	f = 1  
	n = num 
	DO
		IF (MOD(n,i) == 0) THEN 
			factors(f) = i
			f = f+1
			n = n/i
		ELSE
			i = i+1     
		END IF
		IF (n == 1) THEN		
			f = f-1		
			EXIT
		END IF
	END DO
	END SUBROUTINE PRIMEFACTORS
C END FILE PRIMEFACTORS.F
