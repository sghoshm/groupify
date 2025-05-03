// frontend/lib/groupify_app.dart
import 'package:flutter/material.dart';
// Import your screens here

class GroupifyApp extends StatelessWidget {
  const GroupifyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Groupify', // App title
      theme: ThemeData(
        primarySwatch: Colors.blue, // Basic theme color
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      // Define your initial screen or routing here
      home: const HomePage(), // Placeholder for your initial screen
      // Example using named routes:
      // initialRoute: '/',
      // routes: {
      //   '/': (context) => LoginPage(), // Your login screen
      //   '/chat': (context) => ChatListScreen(), // Your chat list screen
      // },
    );
  }
}

// Placeholder Home Page widget
class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Groupify'),
      ),
      body: const Center(
        child: Text('Welcome to Groupify!'),
      ),
    );
  }
}
