package config

import "os"

type JwtConfig struct {
	SecretKey string
}

func LoadJwtConfig() (*JwtConfig, error) {
	return &JwtConfig{
		SecretKey: os.Getenv("SECRET_KEY"),
	}, nil
}
