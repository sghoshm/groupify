#!/usr/bin/env python3
import os
import sys

ROOT = os.getcwd()
LIB = os.path.join(ROOT, "lib")

FILES_TO_CREATE = {
    "lib/screens/welcome_screen.dart": """\
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset('assets/images/welcome.png', height: 250),
              const SizedBox(height: 40),
              const Text(
                'Welcome to Groupify',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              RichText(
                textAlign: TextAlign.center,
                text: TextSpan(
                  style: TextStyle(color: Colors.black87),
                  children: [
                    const TextSpan(text: 'Read our '),
                    TextSpan(
                      text: 'Privacy Policy',
                      style: TextStyle(color: Colors.blue),
                      recognizer: TapGestureRecognizer()
                        ..onTap = () {
                          // TODO
                        },
                    ),
                    const TextSpan(text: '. Tap "Agree & Continue" to accept the '),
                    TextSpan(
                      text: 'Terms of Service',
                      style: TextStyle(color: Colors.blue),
                      recognizer: TapGestureRecognizer()
                        ..onTap = () {
                          // TODO
                        },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/auth-options');
                  },
                  child: const Text('Agree & Continue'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
""",

    "lib/screens/auth/auth_options_screen.dart": """\
import 'package:flutter/material.dart';

class AuthOptionsScreen extends StatelessWidget {
  const AuthOptionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Login or Sign Up")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/login'),
              child: const Text("Continue with Email"),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                // Call backend /auth/google and launch WebView
              },
              child: const Text("Continue with Google"),
            ),
            // Add other providers here
          ],
        ),
      ),
    );
  }
}
""",

    "lib/groupify_app.dart": """\
import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';
import 'screens/auth/auth_options_screen.dart';

class GroupifyApp extends StatelessWidget {
  const GroupifyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Groupify',
      theme: ThemeData(useMaterial3: true),
      initialRoute: '/',
      routes: {
        '/': (context) => const WelcomeScreen(),
        '/auth-options': (context) => const AuthOptionsScreen(),
        // Add more routes later
      },
    );
  }
}
""",

    "lib/main.dart": """\
import 'package:flutter/material.dart';
import 'groupify_app.dart';

void main() {
  runApp(const GroupifyApp());
}
""",

    "lib/services/auth_service.dart": """\
import 'package:dio/dio.dart';

class AuthService {
  final Dio _dio = Dio(BaseOptions(baseUrl: "http://localhost:8000/api/v1/auth"));

  Future<void> login(String email, String password) async {
    final response = await _dio.post("/login", data: {
      "email": email,
      "password": password,
    });

    // TODO: store token securely
    print(response.data);
  }
}
"""
}


def update_pubspec():
    """Ensure required dependencies are in pubspec.yaml."""
    path = os.path.join(ROOT, "pubspec.yaml")
    if not os.path.exists(path):
        print("pubspec.yaml not found.")
        return

    with open(path, "r") as f:
        lines = f.readlines()

    deps_to_add = [
        "provider:",
        "dio:",
        "flutter_secure_storage:"
    ]
    already_present = [line.strip().split(":")[0] for line in lines if ":" in line]
    needs_update = any(dep.split(":")[0] not in already_present for dep in deps_to_add)

    if needs_update:
        with open(path, "a") as f:
            f.write("\ndependencies:\n")
            for dep in deps_to_add:
                f.write(f"  {dep} ^latest\n")  # You can pin versions here
        print("✅ Updated pubspec.yaml with provider, dio, and secure storage.")
    else:
        print("✅ Dependencies already present in pubspec.yaml.")


def safe_write(path, content):
    if os.path.exists(path):
        print(f"🔸 Skipped (already exists): {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Created: {path}")


def main():
    print("🔧 Scaffolding missing Flutter files...")

    for file_path, content in FILES_TO_CREATE.items():
        full_path = os.path.join(ROOT, file_path)
        safe_write(full_path, content)

    update_pubspec()
    print("\n✅ Frontend setup complete. Run `flutter pub get` if needed.")


if __name__ == "__main__":
    main()
