import 'dart:async';
import 'package:flutter/material.dart';
import 'package:app_links/app_links.dart';
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
        debugPrint('Initial deep link error: $e');
      }
    }

    _sub = _appLinks.uriLinkStream.listen(
      (uri) => _handleUri(uri),
      onError: (err) => debugPrint('AppLinks error: $err'),
    );
  }

  Future<void> _handleUri(Uri uri) async {
    debugPrint('📥 Deep link received: $uri');
    if (uri.scheme == 'groupify' && uri.host == 'auth') {
      final code = uri.queryParameters['code'];
      if (code != null) {
        try {
          await AuthService().exchangeOAuthCode(code);
          if (!mounted) return;
          Navigator.pushReplacementNamed(context, '/home');
        } catch (e) {
          if (!mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('OAuth login failed: $e')),
          );
        }
      }
    }
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

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text(
          '🎉 Welcome to Groupify!',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}
