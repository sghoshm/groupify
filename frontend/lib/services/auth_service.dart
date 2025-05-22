import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:dio/dio.dart';

class AuthService {
  final SupabaseClient _client = Supabase.instance.client;

  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://10.0.2.2:8000/api/v1/auth', // FastAPI backend
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));

  Future<void> signup(String email, String password) async {
    final response = await _dio.post('/signup', data: {
      'email': email,
      'password': password,
    });

    if (response.statusCode != 200) {
      throw Exception(
        'Signup failed: ${response.data['detail'] ?? 'Unknown error'}',
      );
    }
  }

  Future<void> startOAuthFlow(String provider) async {
    final supabaseProvider = _getProvider(provider);
    await _client.auth.signInWithOAuth(
      supabaseProvider,
      redirectTo: 'groupify://auth/callback',
    );
  }

  Future<bool> handleOAuthCallback(Uri uri) async {
    final response = await _client.auth.getSessionFromUrl(uri);
    final session = response.session;

    if (session == null || session.user == null) {
      print("❌ OAuth login failed: No session or user.");
      return false;
    }

    print("✅ Logged in as: ${session.user!.email}");
    return true;
  }

  OAuthProvider _getProvider(String provider) {
    switch (provider.toLowerCase()) {
      case 'google':
        return OAuthProvider.google;
      case 'github':
        return OAuthProvider.github;
      case 'facebook':
        return OAuthProvider.facebook;
      case 'microsoft':
      case 'azure':
        return OAuthProvider.azure;
      default:
        throw Exception('Unsupported provider: $provider');
    }
  }

  Future<void> handleDeepLink(Uri uri) async {
    final response = await _client.auth.getSessionFromUrl(uri);
    final session = response.session;

    if (session == null || session.user == null) {
      throw Exception("OAuth login failed: No session or user.");
    }

    print("✅ Logged in as: ${session.user!.email}");
  }

  Future<void> login(String email, String password) async {
    final response = await _dio.post('/login', data: {
      'email': email,
      'password': password,
    });

    if (response.statusCode != 200) {
      throw Exception(
        response.data['detail'] ?? 'Login failed',
      );
    }
  }
}
