package auth

import (
	"fmt"

	"github.com/golang-jwt/jwt/v5"
)

type Validator interface {
	Validate(tokenString string) (jwt.MapClaims, error)
}

type JwtValidator struct {
	secret []byte
}

func NewJwtValidator(secret string) *JwtValidator {
	return &JwtValidator{
		secret: []byte(secret),
	}
}

func (v *JwtValidator) Validate(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return v.secret, nil
	})

	if err != nil {
		return nil, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims, nil
	} else {
		return nil, fmt.Errorf("invalid token")
	}
}
