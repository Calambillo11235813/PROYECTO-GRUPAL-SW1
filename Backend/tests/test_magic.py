try:
    import magic
    print("✅ python-magic importado correctamente")
    
    # Test básico
    test_content = b"Hello World"
    mime_type = magic.from_buffer(test_content, mime=True)
    print(f"✅ MIME detection funciona: {mime_type}")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"⚠️ python-magic importado pero con problemas: {e}")
    print("💡 Solución: Usar versión sin magic")