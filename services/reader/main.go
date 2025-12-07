package main
import (
    "github.com/go-redis/redis/v8"
    "github.com/rs/cors"
    "log"
    "net/http"
)


func main() {
    redisClient := redis.NewClient(&redis.Options{
        Addr: "redis:6379",
    })

    mux := http.NewServeMux()

    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }
        w.Write([]byte("up"))
    })

    mux.HandleFunc("/data", func(w http.ResponseWriter, r *http.Request) {
        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }

        val, err := redisClient.Get(redisClient.Context(), "SHAREDKEY").Result()
        if err != nil {
            w.WriteHeader(http.StatusNotFound)
            w.Write([]byte("key not found"))
            return
        }

        w.Header().Set("Content-Type", "text/plain")
        w.Write([]byte(val))
    })

    handler := cors.New(cors.Options{
        AllowedOrigins: []string{"*"},
        AllowedHeaders: []string{"*"},
    }).Handler(mux)

    log.Println("Reader running on :8082")
    log.Fatal(http.ListenAndServe(":8082", handler))
}
