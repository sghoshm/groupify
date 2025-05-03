// frontend/lib/main.dart
import 'package:flutter/material.dart';
import 'package:groupify/groupify_app.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {
  // Ensure Flutter binding is initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Supabase client
  // Replace with your actual Supabase URL and anon key
  await Supabase.initialize(
    url: "https://nfqnuywfmqqsavalgtdo.supabase.co", // Replace with your Supabase Project URL
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mcW51eXdmbXFxc2F2YWxndGRvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU4NjY2MDEsImV4cCI6MjA2MTQ0MjYwMX0.b-EMiR_hpWY--wqpxO1L11o2-R_nLuYawTFsGKO7qE8', // Replace with your Supabase anon (public) key
  );

  // Run the main application widget
  runApp(const GroupifyApp());
}
