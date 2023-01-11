import 'package:cloud_firestore/cloud_firestore.dart';

class DatabaseService {
  final String? uid;
  DatabaseService({this.uid});

  //reference to collection
  final CollectionReference userCollection =
      FirebaseFirestore.instance.collection("users");
  final CollectionReference groupsCollection =
      FirebaseFirestore.instance.collection("groups");
  //save user data
  Future savingUserData(
      String fullName, String email, String phoneNumber) async {
    return await userCollection.doc(uid).set({
      "fullName": fullName,
      "email": email,
      "phoneNumber": phoneNumber,
      "groups": [],
      "profilePic": "",
      "uid": uid
    });
  }

  //getting user data
  Future gettingUserData(String email) async {
    QuerySnapshot snapshot =
        await userCollection.where("email", isEqualTo: email).get();
    return snapshot;
  }

  //get user groups
  getUserGroups() async {
    return userCollection.doc(uid).snapshots();
  }

  //creating a group
  Future createGroup(String userName, String id, String groupName) async {
    DocumentReference groupDocumentRefernce = await groupsCollection.add({
      "groupName": groupName,
      "groupIcon": "",
      "admin": "${id}_$userName",
      "members": [],
      "groupId": "",
      "recentMessage": "",
      "recentMessageSender": "",
    });
    //updating the group members
    await groupDocumentRefernce.update({
      "members": FieldValue.arrayUnion(["${id}_$userName"]),
      "groupId": groupDocumentRefernce.id
    });
    DocumentReference userDocumentReference = userCollection.doc(uid);
    return await userDocumentReference.update({
      "groups":
          FieldValue.arrayUnion(["${groupDocumentRefernce.id}_$groupName"])
    });
  }

  //getting the chats
  getChats(String groupId) async {
    return groupsCollection
        .doc(groupId)
        .collection("messages")
        .orderBy("time")
        .snapshots();
  }

  Future getGroupAdmin(String groupId) async {
    DocumentReference d = groupsCollection.doc(groupId);
    DocumentSnapshot documentSnapshot = await d.get();
    return documentSnapshot["admin"];
  }

  //getting the group members
  getGroupMembers(groupId) async {
    return groupsCollection.doc(groupId).snapshots();
  }

  //search
  searchByName(String groupName) {
    return groupsCollection.where("groupName", isEqualTo: groupName).get();
  }
}
