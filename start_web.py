#!/usr/bin/env python
# start_web.py - Script pour démarrer l'application web

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Démarrage de l'application ERP Construction")
    print("=" * 60)
    print("\n📱 Accédez à l'application sur : http://localhost:8000")
    print("\n👤 Identifiants de test :")
    print("   - admin / admin123")
    print("   - user / user123")
    print("\n" + "=" * 60)
    print("Appuyez sur CTRL+C pour arrêter le serveur")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main_web:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

