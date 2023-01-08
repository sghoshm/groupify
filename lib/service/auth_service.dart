import 'package:firebase_auth/firebase_auth.dart';
import 'package:groupify/service/database_service.dart';

class AuthService {
  FirebaseAuth firebaseAuth = FirebaseAuth.instance;
  //Login Function

  //Register Function
  Future registerUserWithEmailAndPassword(
      String fullName, String email, String password) async {
    try {
      User user = (await firebaseAuth.createUserWithEmailAndPassword(
              email: email, password: password))
          .user!;
      if (user != null) {
        await DatabaseService(uid: user.uid).updateUserData(fullName, email);
        return true;
      }
    } on FirebaseAuthException catch (e) {
      return e.message;
    }
  }
  //SignOut Function

}
