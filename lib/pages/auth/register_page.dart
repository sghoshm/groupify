import 'package:country_picker/country_picker.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:groupify/helper/helper_function.dart';
import 'package:groupify/pages/auth/login_page.dart';

import 'package:groupify/pages/auth/terms_of_use.dart';
import 'package:groupify/pages/home_page.dart';
import 'package:groupify/service/auth_service.dart';

import '../../widgets/widgets.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({Key? key}) : super(key: key);

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final TextEditingController phoneController = TextEditingController();
  bool _isLoading = false;
  final formKey = GlobalKey<FormState>();
  String email = "";
  String password = "";
  String fullName = "";
  String phoneNumber = "";
  String countryCode = "";
  AuthService authService = AuthService();
  Country selectedCountry = Country(
    phoneCode: '91',
    countryCode: 'IN',
    e164Sc: 0,
    geographic: true,
    level: 1,
    name: 'India',
    example: 'India',
    displayName: 'India',
    displayNameNoCountryCode: 'IN',
    e164Key: '',
  );
  @override
  Widget build(BuildContext context) {
    phoneNumber = phoneController.text;
    countryCode = selectedCountry.phoneCode;
    phoneController.selection = TextSelection.fromPosition(
      TextPosition(
        offset: phoneController.text.length,
      ),
    );
    return Scaffold(
        body: _isLoading
            ? Center(
                child: CircularProgressIndicator(
                    color: Theme.of(context).primaryColor))
            : SingleChildScrollView(
                child: Padding(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 80),
                  child: Form(
                    key: formKey,
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          const Text("GROUPIFY",
                              style: TextStyle(
                                  fontSize: 40, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 10),
                          const Text("Create Your Account Now!",
                              style: TextStyle(
                                  fontSize: 15, fontWeight: FontWeight.w400)),
                          const SizedBox(height: 10),
                          Image.asset("assets/register.png"),
                          const SizedBox(height: 10),
//name
                          TextFormField(
                            decoration: textInputDecoration.copyWith(
                                labelText: "Full Name",
                                prefixIcon: Icon(
                                  Icons.person,
                                  color: Theme.of(context).primaryColor,
                                )),
                            onChanged: (val) {
                              setState(() {
                                fullName = val;
                              });
                            },
                            validator: (val) {
                              if (val!.isNotEmpty) {
                                return null;
                              } else {
                                return "Please Enter Your Name";
                              }
                            },
                          ),
                          const SizedBox(
                            height: 2,
                          ),
//email
                          TextFormField(
                            decoration: textInputDecoration.copyWith(
                                labelText: "Email",
                                prefixIcon: Icon(
                                  Icons.email_rounded,
                                  color: Theme.of(context).primaryColor,
                                )),
                            onChanged: (val) {
                              setState(() {
                                email = val;
                              });
                            },
                            validator: (val) {
                              return RegExp(
                                          r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+")
                                      .hasMatch(val!)
                                  ? null
                                  : "Please enter a valid email";
                            },
                          ),
                          const SizedBox(
                            height: 2,
                          ),
//phone number
                          TextFormField(
                            cursorColor: Theme.of(context).primaryColor,
                            controller: phoneController,
                            keyboardType: TextInputType.phone,
                            onChanged: (val) {
                              setState(() {
                                phoneController.text = val;
                              });
                            },
                            decoration: textInputDecoration.copyWith(
                                labelText: "Mobile Number",
                                prefixIcon: Container(
                                  padding: const EdgeInsets.symmetric(
                                      vertical: 11, horizontal: 10),
                                  child: InkWell(
                                    onTap: () {
                                      showCountryPicker(
                                          context: context,
                                          showPhoneCode: true,
                                          countryListTheme:
                                              const CountryListThemeData(
                                                  bottomSheetHeight: 700),
                                          onSelect: (value) {
                                            setState(() {
                                              selectedCountry = value;
                                            });
                                          });
                                    },
                                    child: Text(
                                      "${selectedCountry.flagEmoji} +${selectedCountry.phoneCode}",
                                      style: const TextStyle(
                                          color: Colors.black,
                                          fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                ),
                                suffixIcon: phoneController.text.length > 9
                                    ? Container(
                                        height: 30,
                                        width: 30,
                                        margin: const EdgeInsets.all(10),
                                        decoration: const BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: Colors.green),
                                        child: const Icon(
                                          Icons.check,
                                          color: Colors.white,
                                          size: 20,
                                        ),
                                      )
                                    : null),
                          ),
// password
                          const SizedBox(
                            height: 2,
                          ),
                          TextFormField(
                            obscureText: true,
                            decoration: textInputDecoration.copyWith(
                                labelText: "Password",
                                prefixIcon: Icon(
                                  Icons.password_rounded,
                                  color: Theme.of(context).primaryColor,
                                )),
                            onChanged: (val) {
                              setState(() {
                                password = val;
                              });
                            },
                            validator: (val) {
                              if (val!.length < 6) {
                                return "Password must be 6 characters.";
                              } else {
                                return null;
                              }
                            },
                          ),
                          const SizedBox(
                            height: 20,
                          ),
                          const TermsOfUse(),
                          SizedBox(
                              width: double.infinity,
                              child: ElevatedButton(
                                style: ElevatedButton.styleFrom(
                                    primary: Theme.of(context).primaryColor,
                                    elevation: 0,
                                    shape: RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(30))),
                                onPressed: (() {
                                  register();
                                  //sendPhoneNumber();
                                  //print("+$countryCode$phoneNumber");
                                }),
                                child: const Text(
                                  "Register",
                                  style: TextStyle(
                                      color: Colors.white, fontSize: 16),
                                ),
                              )),
                          const SizedBox(
                            height: 10,
                          ),
                          Text.rich(TextSpan(
                            text: "Already have an account? ",
                            style: const TextStyle(
                                color: Colors.black, fontSize: 14),
                            children: <TextSpan>[
                              TextSpan(
                                  text: "Login Now",
                                  style: const TextStyle(
                                      color: Colors.black,
                                      decoration: TextDecoration.underline),
                                  recognizer: TapGestureRecognizer()
                                    ..onTap = () {
                                      nextScreen(context, const LoginPage());
                                    }),
                            ],
                          )),
                        ]),
                  ),
                ),
              ));
  }

  /*void sendPhoneNumber() {
    final ap = Provider.of<AuthProvider>(context);
    ap.signInWithPhone(context, "+$countryCode$phoneNumber");
  }*/

  register() async {
    if (formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });
      await authService
          .registerUserWithEmailAndPassword(
              fullName, email, password, phoneNumber, countryCode)
          .then((value) async {
        if (value == true) {
          await HelperFunctions.saveUserLoggedInStatus(true);
          await HelperFunctions.saveUserNameSF(fullName);
          await HelperFunctions.saveUserEmailSF(email);
          await HelperFunctions.saveUserPhoneNumberSF(phoneNumber);
          await HelperFunctions.saveUserCountryCodeSF(countryCode);
          nextScreenReplace(context, const HomePage());
        } else {
          showSnackbar(context, Colors.red, value);
          setState(() {
            _isLoading = false;
          });
        }
      });
    }
  }
}
