import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'groupify_app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Supabase.initialize(
    url:
        'https://nfqnuywfmqqsavalgtdo.supabase.co', // 🔁 Replace with your Supabase URL
    anonKey:
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mcW51eXdmbXFxc2F2YWxndGRvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTg2NjYwMSwiZXhwIjoyMDYxNDQyNjAxfQ.5O4q_MkSHOvY9BSty5U8zldSOQJlVt459IxQyPUvQ1g', // 🔁 Replace with your Supabase anon key
  );

  runApp(const GroupifyApp());
}
