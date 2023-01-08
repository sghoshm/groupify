import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  FirebaseAuth firebaseAuth = FirebaseAuth.instance;
  //Login Function

  //Register Function
  Future registerUserWithEmailAndPassword(
      String fullName, String email, String password) async {
    try {} on FirebaseAuthException catch (e) {}
  }
  //SignOut Function

}
