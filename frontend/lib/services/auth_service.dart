import 'package:dio/dio.dart';

class AuthService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://10.0.2.2:8000/api/v1/auth', // Change IP or domain
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
          'Signup failed: ${response.data['detail'] ?? 'Unknown error'}');
    }
  }

  Future<String> getOAuthUrl(String provider, String redirectTo) async {
    final response = await _dio.get('/$provider', queryParameters: {
      'redirect_to': redirectTo,
    });

    if (response.statusCode == 200 && response.data['auth_url'] != null) {
      return response.data['auth_url'];
    } else {
      throw Exception('Failed to get auth URL for $provider');
    }
  }

  Future<void> exchangeOAuthCode(String code) async {
    final response = await _dio.post(
      '/oauth/exchange',
      data: {'code': code},
      options: Options(
        headers: {
          'Content-Type':
              'application/json', // ✅ Force proper JSON content type
        },
      ),
    );

    if (response.statusCode != 200) {
      throw Exception("OAuth exchange failed: ${response.data['detail']}");
    }

    // Store tokens using flutter_secure_storage later
    print('Session: ${response.data}');
  }
}
