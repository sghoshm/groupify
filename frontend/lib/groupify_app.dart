// groupify_app.dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:app_links/app_links.dart';
import 'package:groupify/screens/auth/login_screen.dart';
import 'package:groupify/screens/home/home_screen.dart';
import 'package:groupify/screens/welcome_screen.dart';
import 'package:groupify/screens/auth/auth_options_screen.dart';
import 'package:groupify/services/auth_service.dart';

class GroupifyApp extends StatelessWidget {
  const GroupifyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Groupify',
      theme: ThemeData(useMaterial3: true),
      initialRoute: '/',
      routes: {
        '/': (context) => const DeepLinkHandlerWrapper(),
        '/auth-options': (context) => const AuthOptionsScreen(),
        '/login': (context) => const LoginScreen(), // ✅ Add this
        '/home': (context) => const HomeScreen(),
      },
    );
  }
}

class DeepLinkHandlerWrapper extends StatefulWidget {
  const DeepLinkHandlerWrapper({super.key});

  @override
  State<DeepLinkHandlerWrapper> createState() => _DeepLinkHandlerWrapperState();
}

class _DeepLinkHandlerWrapperState extends State<DeepLinkHandlerWrapper> {
  late final AppLinks _appLinks;
  StreamSubscription<Uri>? _sub;
  bool _handledInitial = false;

  @override
  void initState() {
    super.initState();
    _appLinks = AppLinks();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _initDeepLinkHandling();
    });
  }

  Future<void> _initDeepLinkHandling() async {
    if (!_handledInitial) {
      try {
        final initial = await _appLinks.getInitialLink();
        if (initial != null) await _handleUri(initial);
        _handledInitial = true;
      } catch (e) {
        debugPrint('Initial deep link error: \$e');
      }
    }

    _sub = _appLinks.uriLinkStream.listen(
      (uri) => _handleUri(uri),
      onError: (err) => debugPrint('AppLinks error: \$err'),
    );
  }

  Future<void> _handleUri(Uri uri) async {
    debugPrint('📥 Deep link received: $uri');
    if (uri.scheme == 'groupify' && uri.host == 'auth') {
      try {
        final success = await AuthService().handleOAuthCallback(uri);
        if (!mounted) return;
        if (success) {
          Navigator.pushReplacementNamed(context, '/home');
        } else {
          _showError('OAuth failed. Please try again without closing the app.');
        }
      } catch (e) {
        if (!mounted) return;
        _showError('OAuth error: $e');
      }
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  void dispose() {
    _sub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return const WelcomeScreen(); // Shown initially while waiting for any link
  }
}
