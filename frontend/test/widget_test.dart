// frontend/test/widget_test.dart
// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:groupify/groupify_app.dart'; // Import your main app file

void main() {
  testWidgets('App starts with basic text', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const GroupifyApp()); // Use the root widget

    // Verify that the basic text widget is present
    expect(find.text('Welcome to Groupify!'), findsOneWidget);
    expect(find.byType(AppBar), findsOneWidget);

    // Add more widget tests here as you develop your UI components
    // Example: Tap a button and verify state change
    // await tester.tap(find.byIcon(Icons.add));
    // await tester.pump();
    // expect(find.text('1'), findsOneWidget);
  });
}
