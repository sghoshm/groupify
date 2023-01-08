import 'package:animations/animations.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:groupify/shared/dialogs/policy_dialog.dart';

class TermsOfUse extends StatelessWidget {
  const TermsOfUse({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(16.0),
        child: RichText(
            text: TextSpan(
                text: "By creating an account, you are agreeing to our\n",
                style: Theme.of(context).textTheme.bodyText1,
                children: [
              TextSpan(
                text: "Terms & Conditions ",
                style: const TextStyle(fontWeight: FontWeight.bold),
                recognizer: TapGestureRecognizer()
                  ..onTap = () {
                    showModal(
                      context: context,
                      configuration: const FadeScaleTransitionConfiguration(),
                      builder: (context) {
                        return PolicyDialog(
                          mdFileName: 'Terms_and_conditions.md',
                        );
                      },
                    );
                  },
              ),
              const TextSpan(text: "and "),
              TextSpan(
                text: "Privacy Policy! ",
                style: const TextStyle(fontWeight: FontWeight.bold),
                recognizer: TapGestureRecognizer()
                  ..onTap = () {
                    showDialog(
                      context: context,
                      builder: (context) {
                        return PolicyDialog(
                          mdFileName: 'privacy_policy.md',
                        );
                      },
                    );
                  },
              ),
            ])));
  }
}
